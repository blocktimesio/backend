import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlatpageDetailComponent } from './flatpage-detail.component';

describe('FlatpageDetailComponent', () => {
  let component: FlatpageDetailComponent;
  let fixture: ComponentFixture<FlatpageDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlatpageDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlatpageDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
