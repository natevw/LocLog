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

- (id)init {
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

@end
