import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlatpageComponent } from './flatpage.component';

describe('FlatpageComponent', () => {
  let component: FlatpageComponent;
  let fixture: ComponentFixture<FlatpageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlatpageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlatpageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
