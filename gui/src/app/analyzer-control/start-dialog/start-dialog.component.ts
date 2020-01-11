import {Component, OnInit} from '@angular/core';
import {AnalyzerControlService, IStartConfig} from "../../services/analyzer-control.service";
import {MatDialogRef} from "@angular/material/dialog";
import {SignsService} from "../../services/signs.service";

@Component({
    selector: 'app-start-dialog',
    templateUrl: './start-dialog.component.html',
    styleUrls: ['./start-dialog.component.css']
})
export class StartDialogComponent implements OnInit {

    startConfig: IStartConfig = {
        action: "start",
        reader: "interface",
        home_network: "192.168.0.0/24",
        external_network: "0.0.0.0/0",
        signs: []
    };

    constructor(private analyzerControlService: AnalyzerControlService,
                private signsService: SignsService,
                private dialogRef: MatDialogRef<StartDialogComponent>) {
    }

    ngOnInit() {
    }

    saveChanges() {
        this.signsService.getSigns().subscribe(res => {
            this.startConfig.signs = res;
            this.analyzerControlService.startAnalyzer(this.startConfig).subscribe(res => {
                this.dialogRef.close(true)
            })
        })
    }

    cancel() {
        this.dialogRef.close(false)
    }

}
