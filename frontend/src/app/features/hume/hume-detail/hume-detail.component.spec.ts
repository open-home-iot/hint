import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HumeDetailComponent } from './hume-detail.component';

describe('HumeDetailComponent', () => {
  let component: HumeDetailComponent;
  let fixture: ComponentFixture<HumeDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HumeDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HumeDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
