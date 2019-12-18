import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AnalyzerControlComponent } from './analyzer-control.component';

describe('AnalyzerControlComponent', () => {
  let component: AnalyzerControlComponent;
  let fixture: ComponentFixture<AnalyzerControlComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AnalyzerControlComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AnalyzerControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
