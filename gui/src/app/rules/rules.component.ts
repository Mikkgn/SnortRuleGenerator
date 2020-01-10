import {Component, OnInit} from '@angular/core';
import {RulesService} from "../services/rules.service";
import {animate, state, style, transition, trigger} from "@angular/animations";

@Component({
    selector: 'app-rules',
    templateUrl: './rules.component.html',
    styleUrls: ['./rules.component.css'],
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({height: '0px', minHeight: '0'})),
            state('expanded', style({height: '*'})),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ],
})
export class RulesComponent implements OnInit {

    rules: string[] = [];
    columnsToDisplay: string[] = [
        'rule',
    ];

    constructor(private rulesService: RulesService) {
    }

    ngOnInit() {
        this.rulesService.getRules().subscribe(res => {
            this.rules = res;
        })
    }

    downloadRules() {
        const filename = 'localrules';
        const blob = new Blob([this.rules.join('\n')], {type: 'text/plain'});
        if (window.navigator && window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveOrOpenBlob(blob, filename);
        } else {
            var e = document.createEvent('MouseEvents'),
                a = document.createElement('a');
            a.download = filename;
            a.href = window.URL.createObjectURL(blob);
            a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
            e.initEvent('click', true, false);
            a.dispatchEvent(e);
            window.URL.revokeObjectURL(a.href); // clean the url.createObjectURL resource
        }
    }

    clear() {
        this.rulesService.deleteRules().subscribe(() => {
        });
        this.rules = [];
    }
}
