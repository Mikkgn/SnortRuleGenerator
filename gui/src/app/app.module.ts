import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {StompService} from '@stomp/ng2-stompjs';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {NavigationComponent} from './navigation/navigation.component';
import {MatMenuModule} from '@angular/material/menu';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import {DefinitionsComponent} from './definitions/definitions.component';
import {RouterModule} from '@angular/router';
import {MatTableModule} from '@angular/material/table';
import {AnalyzerControlComponent} from './analyzer-control/analyzer-control.component';
import {EventsComponent} from './events/events.component';
import {MatCardModule} from "@angular/material/card";
import {MatBadgeModule} from "@angular/material/badge";
import {PrettyPrintPipe} from "./pretty-print.pipe";
import {RulesComponent} from "./rules/rules.component";
import {RulesService} from "./services/rules.service";
import {AnalyzerControlService} from "./services/analyzer-control.service";
import {EventsService} from "./services/events.service";
import {SignsService} from "./services/signs.service";
import {MatSnackBarModule} from "@angular/material/snack-bar";
import {MatDialogModule} from "@angular/material/dialog";
import {StartDialogComponent} from './analyzer-control/start-dialog/start-dialog.component';
import {CreateNewDialogComponent} from './definitions/create-new-dialog/create-new-dialog.component';
import {MatSelectModule} from "@angular/material/select";
import {MatInputModule} from "@angular/material/input";


@NgModule({
    declarations: [
        AppComponent,
        NavigationComponent,
        DefinitionsComponent,
        AnalyzerControlComponent,
        EventsComponent,
        PrettyPrintPipe,
        RulesComponent,
        StartDialogComponent,
        CreateNewDialogComponent,
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
        MatTableModule,
        MatCardModule,
        MatBadgeModule,
        MatSnackBarModule,
        MatDialogModule,
        MatSelectModule,
        MatInputModule
    ],
    providers: [
        StompService,
        RulesService,
        AnalyzerControlService,
        EventsService,
        SignsService,
    ],
    bootstrap: [
        AppComponent,
        NavigationComponent
    ],
    entryComponents: [NavigationComponent, StartDialogComponent, CreateNewDialogComponent]
})
export class AppModule {
}

platformBrowserDynamic().bootstrapModule(AppModule)
    .catch(err => console.error(err));
