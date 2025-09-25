import { TestBed } from '@angular/core/testing';

import { EmailClassificationService } from './email-classification.service';

describe('EmailClassificationService', () => {
  let service: EmailClassificationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EmailClassificationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
