import {Component, OnInit} from '@angular/core';
import {AnalyzerControlService} from "../services/analyzer-control.service";
import {MatSnackBar} from "@angular/material/snack-bar";
import {MatDialog} from "@angular/material/dialog";
import {StartDialogComponent} from "./start-dialog/start-dialog.component";

@Component({
    selector: 'app-analyzer-control',
    templateUrl: './analyzer-control.component.html',
    styleUrls: ['./analyzer-control.component.scss']
})
export class AnalyzerControlComponent implements OnInit {

    currentState: { status: 'ACTIVE' | 'DISABLED' } = {
        status: 'DISABLED'
    };

    constructor(private analyzerControlService: AnalyzerControlService,
                private snackBar: MatSnackBar,
                private matDialog: MatDialog) {
    }

    ngOnInit() {
        this.getStatusAnalyzer();
    }

    stopAnalyzer() {
        this.analyzerControlService.stopAnalyzer().subscribe(() => {
            this.snackBar.open('Command for stop analyzer successfully send', 'Close', {
                duration: 2000,
                verticalPosition: "top"
            });
            this.getStatusAnalyzer();
        })
    }

    getStatusAnalyzer() {
        this.analyzerControlService.getStatusAnalyzer().subscribe(res => {
            this.currentState = res;
        })
    }

    openStartDialog() {
        const matDialogRef = this.matDialog.open(StartDialogComponent, {width: '300px'});
        matDialogRef.afterClosed().subscribe((res) => {
            this.getStatusAnalyzer();
            if (res) {
                this.snackBar.open('Command for start analyzer successfully send', 'Close', {
                    duration: 2000,
                    verticalPosition: "top"
                });
            }
        })
    }
}
