import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {StompConfig, StompService} from "@stomp/ng2-stompjs";

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
        AppComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
    ],
    providers: [
        StompService,
        {
            provide: StompConfig,
            useValue: stompConfig
        }
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
