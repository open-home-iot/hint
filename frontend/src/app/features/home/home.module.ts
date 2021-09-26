import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

// PAGES
import { HomeOverviewComponent } from './pages/home-overview/home-overview.component';

// SERVICES
import { HomeService } from './home.service';

// MODULES
import { HomeRoutingModule } from './home-routing.module';
import { HumeModule } from '../hume/hume.module';
import { DeviceModule } from '../device/device.module';

// COMPONENTS
import { HomeAddComponent } from './home-add/home-add.component';
import { HomeListComponent } from './home-list/home-list.component';
import { RoomAddComponent } from './room-add/room-add.component';
import { HomeDetailComponent } from './home-detail/home-detail.component';
import { HomeSelectComponent } from './home-select/home-select.component';


@NgModule({
  declarations: [
    HomeOverviewComponent,
    HomeAddComponent,
    HomeListComponent,
    RoomAddComponent,
    HomeDetailComponent,
    HomeSelectComponent
  ],
  imports: [
    HomeRoutingModule,
    CommonModule,
    ReactiveFormsModule,
    HumeModule,
    DeviceModule
  ],
  exports: [
    HomeOverviewComponent
  ],
  providers: [HomeService]
})
export class HomeModule {}
