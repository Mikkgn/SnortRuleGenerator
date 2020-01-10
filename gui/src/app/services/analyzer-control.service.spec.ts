import { TestBed } from '@angular/core/testing';

import { AnalyzerControlService } from './analyzer-control.service';

describe('AnalyzerControlService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: AnalyzerControlService = TestBed.get(AnalyzerControlService);
    expect(service).toBeTruthy();
  });
});
