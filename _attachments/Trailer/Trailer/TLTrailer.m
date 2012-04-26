//
//  TLTrailer.m
//  Trailer
//
//  Created by Nathan Vander Wilt on 4/21/12.
//  Copyright (c) 2012 &yet. All rights reserved.
//

#import "TLTrailer.h"



@implementation TLTrailer

@synthesize locManager = _locManager;
@synthesize currentSequence = _currentSequence;
@synthesize db = _db;
@synthesize insertLoc = _insertLoc;

- (id)init {
	NSString *documentsDir = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
	NSString *databasePath = [documentsDir stringByAppendingPathComponent:@"trailer-v1.sqlite3"];
    
    sqlite3_open([databasePath fileSystemRepresentation], &_db);
    sqlite3_exec(self.db, "CREATE TABLE IF NOT EXISTS location_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB)", NULL, NULL, NULL);
    
    // fetch latest sequence id, thanks http://stackoverflow.com/a/5301923/179583
    sqlite3_stmt* q;
    sqlite3_prepare_v2(self.db, "SELECT seq FROM SQLITE_SEQUENCE WHERE name='location_logs'", -1, &q, NULL);
    sqlite3_step(q);
    _currentSequence = sqlite3_column_int64(q, 0);
    sqlite3_finalize(q);
    
    sqlite3_prepare_v2(self.db, "INSERT INTO location_logs (data) VALUES (?)", -1, &_insertLoc, NULL);
    
    // TODO: use NSUserDefaults to store/re-set last selected states
    _locManager = [CLLocationManager new];
    self.locManager.delegate = self;
    self.locManager.desiredAccuracy = kCLLocationAccuracyBest;
    [self.locManager startUpdatingLocation];
    return self;
}

- (void)dealloc {
    sqlite3_finalize(self.insertLoc);
    sqlite3_close(self.db);
}

- (void)locationManager:(CLLocationManager *)manager didFailWithError:(NSError *)error
{
    NSLog(@"Error: %@", error);
}

- (void)locationManager:(CLLocationManager *)manager didUpdateToLocation:(CLLocation *)newLocation fromLocation:(CLLocation *)oldLocation
{
    NSData* locData = [NSKeyedArchiver archivedDataWithRootObject:newLocation];
    sqlite3_bind_blob(self.insertLoc, 1, [locData bytes], [locData length], SQLITE_STATIC);
    sqlite3_step(self.insertLoc);
    sqlite3_reset(self.insertLoc);
    sqlite3_clear_bindings(self.insertLoc);
    [locData self]; // make sure data retained until insertion is done
    _currentSequence = sqlite3_last_insert_rowid(self.db);
}

- (NSArray*)updatesSince:(TLTrailerSequence)seq {
    sqlite3_stmt* q;
    sqlite3_prepare_v2(self.db, "SELECT data FROM location_logs WHERE id > ?", -1, &q, NULL);
    sqlite3_bind_int64(q, 1, seq);
    
    NSMutableArray* updates = [NSMutableArray array];
    while (sqlite3_step(q) == SQLITE_ROW) {
        NSData* locArchive = [NSData dataWithBytesNoCopy:(void*)sqlite3_column_blob(q, 0)
                                                  length:sqlite3_column_bytes(q, 0)
                                            freeWhenDone:NO];
        CLLocation* loc = [NSKeyedUnarchiver unarchiveObjectWithData:locArchive];
        [updates addObject:loc];
    }
    return updates;
}
- (void)removeUpdatesThrough:(TLTrailerSequence)seq {
    char* sql = sqlite3_mprintf("DELETE FROM location_logs WHERE id <= %i", seq);
    sqlite3_exec(self.db, sql, NULL, NULL, NULL);
    sqlite3_free(sql);
}

@end
