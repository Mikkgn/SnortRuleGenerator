import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MatMenuModule} from '@angular/material/menu';
import {DefinitionsComponent} from './definitions/definitions.component';
import {EventsComponent} from './events/events.component';
import {AnalyzerControlComponent} from './analyzer-control/analyzer-control.component';
import {RulesComponent} from "./rules/rules.component";

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
    },
    {
        path: 'rules',
        component: RulesComponent
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
