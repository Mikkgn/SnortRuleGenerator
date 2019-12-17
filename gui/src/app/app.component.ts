import {Component, OnInit} from '@angular/core';
import {StompService} from "@stomp/ng2-stompjs";
import {map} from "rxjs/operators";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
    title = 'gui';

    constructor(private stompService: StompService) {
    }

    ngOnInit(): void {
        let stomp_subscription = this.stompService.subscribe('/queue/events');

        stomp_subscription.pipe(map((message) => {
            return message.body;
        })).subscribe((msg_body: string) => {
            console.log(`Received: ${msg_body}`);
        });
    }
}
