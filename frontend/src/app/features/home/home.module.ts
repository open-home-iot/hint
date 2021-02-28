import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

// COMPONENTS
import { HomeAddComponent } from './home-add/home-add.component';
import { HomeListComponent } from './home-list/home-list.component';

// PAGES
import { HomeOverviewComponent } from './pages/home-overview/home-overview.component';
import { HomeRoomOverviewComponent } from './pages/home-room-overview/home-room-overview.component';

// SERVICES
import { HomeService } from './home.service';

// MODULES
import { HomeRoutingModule } from './home-routing.module';
import { HumeModule } from '../hume/hume.module';
import { HomeRoomAddComponent } from './home-room-add/home-room-add.component';


@NgModule({
  declarations: [
    HomeOverviewComponent,
    HomeAddComponent,
    HomeListComponent,
    HomeRoomAddComponent,
    HomeRoomOverviewComponent
  ],
  imports: [
    HomeRoutingModule,
    CommonModule,
    ReactiveFormsModule,
    HumeModule
  ],
  exports: [
    HomeOverviewComponent
  ],
  providers: [HomeService]
})
export class HomeModule {}
