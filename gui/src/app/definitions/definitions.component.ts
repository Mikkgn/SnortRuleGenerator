import {Component, OnInit} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {ISign, SignsService} from "../services/signs.service";
import {MatDialog} from "@angular/material/dialog";
import {CreateNewDialogComponent} from "./create-new-dialog/create-new-dialog.component";

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

    signs: ISign[] = [];
    columnsToDisplay: string[] = [
        'name',
        'src',
        'dst',
        'result_criteria',
        'delete_button'
    ];
    expandedElement: any | null;

    constructor(private signsService: SignsService, private matDialog: MatDialog) {
    }

    ngOnInit() {
        this.getSigns()
    }

    getSigns() {
        this.signsService.getSigns().subscribe(res => {
            this.signs = res as ISign[];
        })
    }

    openNewDialog() {
        const matDialogRef = this.matDialog.open(CreateNewDialogComponent, {width: '400px'});
        matDialogRef.afterClosed().subscribe(() => {
            this.getSigns()
        })
    }

    deleteSign(sign: ISign) {
        this.signsService.deleteSign(sign.id).subscribe(() => {
            this.getSigns()
        })
    }

}
