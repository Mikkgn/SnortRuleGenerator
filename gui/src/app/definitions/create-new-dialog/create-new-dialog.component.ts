import {Component, OnInit} from '@angular/core';
import {ISign, SignsService} from "../../services/signs.service";
import {MatDialogRef} from "@angular/material/dialog";

@Component({
    selector: 'app-create-new-dialog',
    templateUrl: './create-new-dialog.component.html',
    styleUrls: ['./create-new-dialog.component.css']
})
export class CreateNewDialogComponent implements OnInit {

    newSign: ISign = {
        name: '',
        checked_fields: [
            {
                request_uri: 'somethin_there',
                search_type: 'REGEX'
            }
        ],
        src: 'EXTERNAL',
        dst: 'HOME',
        packet_type: 'HTTP',
        result_criteria: 'AT_LEAST_ONE'
    };


    constructor(private signsService: SignsService, private dialogRef: MatDialogRef<CreateNewDialogComponent>) {
    }

    ngOnInit() {
    }

    saveChanges() {
        this.signsService.addSign(this.newSign).subscribe(() => {
            this.dialogRef.close()
        })
    }

    changeJson(str: string) {
        console.log(str);
        this.newSign.checked_fields = JSON.parse(str);
    }

    getJsonValue(){
        return JSON.stringify(this.newSign.checked_fields)
    }

}
