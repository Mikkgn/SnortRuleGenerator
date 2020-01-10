import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {BaseUrl} from "../app.component";

@Injectable({
  providedIn: 'root'
})
export class AnalyzerControlService {

    constructor(private http: HttpClient) {
    }

    startAnalyzer(): Observable<{}[]> {
        return this.http.get<{}[]>(BaseUrl + '/signs', {params: {offset: '0', limit: '1000'}})
    }

    getStatusAnalyzer(): Observable<{status: string}> {
        return this.http.get<{status: string}>(BaseUrl + '/analyzer/status')
    }

    stopAnalyzer(): Observable<undefined> {
        return this.http.post<undefined>(BaseUrl + '/analyzer/stop', {})
    }

}
