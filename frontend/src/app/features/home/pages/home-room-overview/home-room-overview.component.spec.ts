import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeRoomOverviewComponent } from './home-room-overview.component';

describe('HomeRoomOverviewComponent', () => {
  let component: HomeRoomOverviewComponent;
  let fixture: ComponentFixture<HomeRoomOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomeRoomOverviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeRoomOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
