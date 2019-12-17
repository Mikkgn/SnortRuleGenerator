import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MatMenuModule} from "@angular/material/menu";

const routes: Routes = [];

@NgModule({
    imports: [
        RouterModule.forRoot(routes),
        MatMenuModule
    ],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
