import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeRoomAddComponent } from './home-room-add.component';

describe('HomeRoomAddComponent', () => {
  let component: HomeRoomAddComponent;
  let fixture: ComponentFixture<HomeRoomAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomeRoomAddComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeRoomAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
