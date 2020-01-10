import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {BaseUrl} from "../app.component";

@Injectable({
    providedIn: 'root'
})
export class RulesService {

    constructor(private http: HttpClient) {
    }


    getRules(): Observable<string[]> {
        return this.http.get<string[]>(BaseUrl + '/rules')
    }

    downloadRules() {
        return
    }

    deleteRules(): Observable<undefined> {
        return this.http.delete<undefined>(BaseUrl + '/rules')
    }

}
