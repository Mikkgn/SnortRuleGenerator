import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {BaseUrl} from "../app.component";

@Injectable({
    providedIn: 'root'
})
export class AnalyzerControlService {

    constructor(private http: HttpClient) {
    }

    startAnalyzer(startConfig: IStartConfig): Observable<{}[]> {
        return this.http.post<{}[]>(BaseUrl + '/analyzer/start', startConfig)
    }

    getStatusAnalyzer(): Observable<{ status: "ACTIVE" | "DISABLED" }> {
        return this.http.get<{ status: "ACTIVE" | "DISABLED" }>(BaseUrl + '/analyzer/status')
    }

    stopAnalyzer(): Observable<undefined> {
        return this.http.post<undefined>(BaseUrl + '/analyzer/stop', {})
    }

}

export interface IStartConfig {
    reader: "pcap" | "interface";
    action: "start";
    home_network: string;
    external_network: string;
    signs: {}[];
    filename?: string;
    interface_name?: string;
}
