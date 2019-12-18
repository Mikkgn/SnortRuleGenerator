import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MatMenuModule} from '@angular/material/menu';
import {DefinitionsComponent} from './definitions/definitions.component';
import {EventsComponent} from './events/events.component';
import {AnalyzerControlComponent} from './analyzer-control/analyzer-control.component';

const routes: Routes = [
    {
        path: 'definitions',
        component: DefinitionsComponent
    },
    {
        path: 'events',
        component: EventsComponent
    },
    {
        path: 'analyzer_control',
        component: AnalyzerControlComponent
    }
];

@NgModule({
    imports: [
        RouterModule.forRoot(routes),
        MatMenuModule
    ],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
