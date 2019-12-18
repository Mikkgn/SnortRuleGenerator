import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {StompConfig, StompService} from '@stomp/ng2-stompjs';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {NavigationComponent} from './navigation/navigation.component';
import {MatMenuModule} from '@angular/material/menu';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import { DefinitionsComponent } from './definitions/definitions.component';
import {RouterModule} from '@angular/router';
import {MatTableModule} from '@angular/material/table';
import { AnalyzerControlComponent } from './analyzer-control/analyzer-control.component';
import { EventsComponent } from './events/events.component';

const stompConfig: StompConfig = {
    // Which server?
    url: 'ws://192.168.99.100:15674/ws',

    // Headers
    // Typical keys: login, passcode, host
    headers: {
        login: 'root',
        passcode: 'P@ssword'
    },

    // How often to heartbeat?
    // Interval in milliseconds, set to 0 to disable
    heartbeat_in: 0, // Typical value 0 - disabled
    heartbeat_out: 20000, // Typical value 20000 - every 20 seconds

    // Wait in milliseconds before attempting auto reconnect
    // Set to 0 to disable
    // Typical value 5000 (5 seconds)
    reconnect_delay: 5000,

    // Will log diagnostics on console
    debug: true
};

@NgModule({
    declarations: [
        AppComponent,
        NavigationComponent,
        DefinitionsComponent,
        AnalyzerControlComponent,
        EventsComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        FormsModule,
        HttpClientModule,
        ReactiveFormsModule,
        MatMenuModule,
        MatIconModule,
        MatButtonModule,
        MatToolbarModule,
        RouterModule,
        MatTableModule
    ],
    providers: [
        StompService,
        {
            provide: StompConfig,
            useValue: stompConfig
        }
    ],
    bootstrap: [
        AppComponent,
        NavigationComponent
    ],
    entryComponents: [NavigationComponent]
})
export class AppModule {
}

platformBrowserDynamic().bootstrapModule(AppModule)
    .catch(err => console.error(err));
