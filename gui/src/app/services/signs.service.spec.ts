import { TestBed } from '@angular/core/testing';

import { SignsService } from './signs.service';

describe('SignsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SignsService = TestBed.get(SignsService);
    expect(service).toBeTruthy();
  });
});
