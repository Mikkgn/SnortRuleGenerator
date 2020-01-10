import {Component, OnInit} from '@angular/core';
import {AnalyzerControlService} from "../services/analyzer-control.service";

@Component({
    selector: 'app-analyzer-control',
    templateUrl: './analyzer-control.component.html',
    styleUrls: ['./analyzer-control.component.scss']
})
export class AnalyzerControlComponent implements OnInit {

    currentState = {
        status: 'DISABLED'
    };

    constructor(private analyzerControlService: AnalyzerControlService) {
    }

    ngOnInit() {
        this.analyzerControlService.getStatusAnalyzer().subscribe(res => {
            this.currentState = res;
        })
    }

}
