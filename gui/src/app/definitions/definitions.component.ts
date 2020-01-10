import {Component, OnInit} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {SignsService} from "../services/signs.service";

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

    signs: {}[] = [];
    columnsToDisplay: string[] = [
        'name',
        'src',
        'dst',
        'result_criteria'
    ];
    expandedElement: any | null;

    constructor(private signsService: SignsService) {
    }

    ngOnInit() {
        this.signsService.getSigns().subscribe(res => {
            this.signs = res;
        })
    }

}
