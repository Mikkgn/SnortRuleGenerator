import {Component, OnInit} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';

@Component({
    selector: 'app-definitions',
    templateUrl: './definitions.component.html',
    styleUrls: ['./definitions.component.scss'],
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({height: '0px', minHeight: '0'})),
            state('expanded', style({height: '*'})),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ],
})
export class DefinitionsComponent implements OnInit {

    definitions: { id: number, name: string }[] = [
        {id: 1, name: 'test1'}, {id: 2, name: 'test'}
    ];
    columnsToDisplay: string[] = [
        'name',
        'description'
    ];
    expandedElement: any | null;

    constructor() {
    }

    ngOnInit() {
    }

}
