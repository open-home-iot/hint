import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HumeListComponent } from './hume-list.component';

describe('HumeListComponent', () => {
  let component: HumeListComponent;
  let fixture: ComponentFixture<HumeListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HumeListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HumeListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
