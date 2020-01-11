import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {BaseUrl} from "../app.component";
import {Observable} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class SignsService {

    constructor(private http: HttpClient) {
    }


    getSigns(): Observable<{}[]> {
        return this.http.get<{}[]>(BaseUrl + '/signs', {params: {offset: '0', limit: '1000'}})
    }

    addSign(sign: ISign): Observable<ISign> {
        return this.http.post<ISign>(BaseUrl + '/signs', sign)
    }

    deleteSign(signId: string): Observable<undefined> {
        return this.http.delete<undefined>(BaseUrl + '/signs/' + signId)
    }
}


export interface ISign {
    id?: string;
    name: string;
    checked_fields: {}[];
    result_criteria: 'ALL' | 'AT_LEAST_ONE';
    src: 'EXTERNAL' | 'HOME';
    dst: 'EXTERNAL' | 'HOME';
    packet_type: 'HTTP' | 'TCP' | 'IP'
}
