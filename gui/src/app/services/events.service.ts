import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {BaseUrl} from "../app.component";

@Injectable({
    providedIn: 'root'
})
export class EventsService {

    constructor(private http: HttpClient) {
    }


    getEvents(): Observable<{}[]> {
        return this.http.get<{}[]>(BaseUrl + '/events', {params: {offset: '0', limit: '1000'}})
    }

}
