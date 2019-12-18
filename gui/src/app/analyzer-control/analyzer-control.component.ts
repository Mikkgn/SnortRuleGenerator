import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-analyzer-control',
  templateUrl: './analyzer-control.component.html',
  styleUrls: ['./analyzer-control.component.scss']
})
export class AnalyzerControlComponent implements OnInit {

    currentState = {
        state: 'ACTIVE',
        mode: 'interface',
        params: 'eth0'
    };

  constructor() { }

  ngOnInit() {
  }

}
