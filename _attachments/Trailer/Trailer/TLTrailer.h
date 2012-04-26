//
//  TLTrailer.h
//  Trailer
//
//  Created by Nathan Vander Wilt on 4/21/12.
//  Copyright (c) 2012 &yet. All rights reserved.
//

#import <Foundation/Foundation.h>

#import <CoreLocation/CoreLocation.h>
#include <sqlite3.h>

typedef NSUInteger TLTrailerSequence;

@interface TLTrailer : NSObject <CLLocationManagerDelegate> 

@property (strong, readonly) CLLocationManager *locManager;
@property (readonly) sqlite3* db;
@property (readonly) sqlite3_stmt* insertLoc;


@property (readonly) TLTrailerSequence currentSequence;
- (NSArray*)updatesSince:(TLTrailerSequence)seq;
- (void)removeUpdatesThrough:(TLTrailerSequence)seq;

@end
