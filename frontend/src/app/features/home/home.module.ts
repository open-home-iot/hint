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
import { HomeSelectComponent } from './home-select/home-select.component';
import { HomeEditComponent } from './home-select/home-edit/home-edit.component';


@NgModule({
  declarations: [
    HomeOverviewComponent,
    HomeAddComponent,
    HomeSelectComponent,
    HomeEditComponent
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
