import {Component, OnInit} from '@angular/core';
import {animate, state, style, transition, trigger} from "@angular/animations";
import {EventsService} from "../services/events.service";

@Component({
    selector: 'app-events',
    templateUrl: './events.component.html',
    styleUrls: ['./events.component.css'],
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({height: '0px', minHeight: '0'})),
            state('expanded', style({height: '*'})),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ],
})
export class EventsComponent implements OnInit {

    events: {}[] = [];
    columnsToDisplay: string[] = [
        'sign_name',
        'created_at'
    ];
    expandedElement: any | null;

    constructor(private eventsService: EventsService) {
    }

    ngOnInit() {
        this.eventsService.getEvents().subscribe(res => {
            this.events = res;
        })
    }
}
