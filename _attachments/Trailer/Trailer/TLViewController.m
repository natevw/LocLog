//
//  TLViewController.m
//  Trailer
//
//  Created by Nathan Vander Wilt on 4/12/12.
//  Copyright (c) 2012 &yet. All rights reserved.
//

#import "TLViewController.h"

#import "TLAppDelegate.h"

@implementation TLViewController

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (void)viewWillAppear:(BOOL)animated
{
    [super viewWillAppear:animated];
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
}

- (void)viewWillDisappear:(BOOL)animated
{
	[super viewWillDisappear:animated];
}

- (void)viewDidDisappear:(BOOL)animated
{
	[super viewDidDisappear:animated];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (CLLocationManager*)locationManager {
    TLAppDelegate *appDelegate = (TLAppDelegate *)[UIApplication sharedApplication].delegate;
    return appDelegate.logger.locManager;
}

// TODO: these settings need to be persisted, restored and properly applied on app load

- (IBAction)changeLogging:(UISwitch *)loggingSwitch {
    if (loggingSwitch.isOn) [[self locationManager] startUpdatingLocation];
    else [[self locationManager] stopUpdatingLocation];
}

- (IBAction)changeSending:(id)sender {}

- (IBAction)changeAccuracy:(UISegmentedControl *)accuracyChooser {
    CLLocationAccuracy options[] = {kCLLocationAccuracyThreeKilometers, kCLLocationAccuracyHundredMeters, kCLLocationAccuracyNearestTenMeters, kCLLocationAccuracyBest};
    [self locationManager].desiredAccuracy = options[accuracyChooser.selectedSegmentIndex];
    NSLog(@"Accuracy now: %f", [self locationManager].desiredAccuracy);
}



@end
