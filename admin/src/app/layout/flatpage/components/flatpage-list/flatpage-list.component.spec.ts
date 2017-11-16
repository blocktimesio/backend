import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlatpageListComponent } from './flatpage-list.component';

describe('FlatpageListComponent', () => {
  let component: FlatpageListComponent;
  let fixture: ComponentFixture<FlatpageListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlatpageListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlatpageListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
