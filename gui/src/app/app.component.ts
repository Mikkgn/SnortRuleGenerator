import {Component, OnInit} from '@angular/core';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})


export class AppComponent implements OnInit {
    title = 'gui';

    constructor() {
    }

    ngOnInit(): void {
        // let stomp_subscription = this.stompService.subscribe('/queue/events');
        //
        // stomp_subscription.pipe(map((message) => {
        //     return message.body;
        // })).subscribe((msg_body: string) => {
        //     console.log(`Received: ${msg_body}`);
        // });
    }
}

export const BaseUrl = location.origin + ':8080';
