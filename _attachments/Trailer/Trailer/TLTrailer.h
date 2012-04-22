//
//  TLTrailer.h
//  Trailer
//
//  Created by Nathan Vander Wilt on 4/21/12.
//  Copyright (c) 2012 &yet. All rights reserved.
//

#import <Foundation/Foundation.h>

#import <CoreLocation/CoreLocation.h>

typedef NSUInteger TLTrailerSequence;

@interface TLTrailer : NSObject <CLLocationManagerDelegate> 

@property (strong, nonatomic) CLLocationManager *locManager;

@property (readonly) TLTrailerSequence currentSequence;
- (NSArray*)updatesUntil:(TLTrailerSequence)seq;
- (void)removeUpdates:(TLTrailerSequence)seq;

@end
