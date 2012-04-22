//
//  TLTrailer.m
//  Trailer
//
//  Created by Nathan Vander Wilt on 4/21/12.
//  Copyright (c) 2012 &yet. All rights reserved.
//

#import "TLTrailer.h"
#include <sqlite3.h>


@implementation TLTrailer

@synthesize locManager = _locManager;
@synthesize currentSequence = _currentSequence;

- (id)init {
	NSString *documentsDir = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
	NSString *databasePath = [documentsDir stringByAppendingPathComponent:@"trailer-v1.sqlite3"];

    sqlite3* db;
    sqlite3_open([databasePath fileSystemRepresentation], &db);
    sqlite3_exec(db, "CREATE TABLE IF NOT EXISTS location_logs(data TEXT)", NULL, NULL, NULL);
    
    // fetch latest sequence id, thanks http://stackoverflow.com/a/5301923/179583
    sqlite3_stmt* q;
    sqlite3_prepare_v2(db, "SELECT seq FROM SQLITE_SEQUENCE WHERE name='location_logs'", -1, &q, NULL);
    sqlite3_step(q);
    _currentSequence = sqlite3_column_int(q, 0);
    sqlite3_finalize(q);
    
    // TODO: keep this handy for later instead...
    sqlite3_close(db);
    
    // TODO: use NSUserDefaults to store/re-set last selected states
    self.locManager = [CLLocationManager new];
    self.locManager.delegate = self;
    self.locManager.desiredAccuracy = kCLLocationAccuracyBest;
    [self.locManager startUpdatingLocation];
    return self;
}

- (void)locationManager:(CLLocationManager *)manager didFailWithError:(NSError *)error
{
    NSLog(@"Error: %@", error);
}

- (void)locationManager:(CLLocationManager *)manager didUpdateToLocation:(CLLocation *)newLocation fromLocation:(CLLocation *)oldLocation
{
    NSLog(@"Update: %@", newLocation);
}

- (NSArray*)updatesUntil:(TLTrailerSequence)seq  { return nil; }
- (void)removeUpdates:(TLTrailerSequence)seq {}

@end
