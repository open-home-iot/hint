import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { DeviceListComponent } from './device-list/device-list.component';
import { DeviceDetailComponent } from './device-detail/device-detail.component';
import { DeviceDiscoverComponent } from './device-discover/device-discover.component';

// PAGES

// SERVICES
import { DeviceService } from './device.service';

// MODULES
import { DeviceRoutingModule } from './device-routing.module';
import { DeviceDiscoveredComponent } from './device-discovered/device-discovered.component';


@NgModule({
  declarations: [
    DeviceListComponent,
    DeviceDetailComponent,
    DeviceDiscoverComponent,
    DeviceDiscoveredComponent,
  ],
  imports: [
    DeviceRoutingModule,
    CommonModule
  ],
  exports: [
    DeviceListComponent,
    DeviceDiscoverComponent
  ],
  providers: [DeviceService]
})
export class DeviceModule {}
