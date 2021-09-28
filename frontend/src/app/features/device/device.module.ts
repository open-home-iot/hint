import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { HomeDevicesComponent } from './home-devices/home-devices.component';
import { RoomDevicesComponent } from './room-devices/room-devices.component';
import { DeviceListComponent } from './device-list/device-list.component';
import { DeviceDetailComponent } from './device-detail/device-detail.component';
import { DeviceRoomSelectorComponent } from './device-room-selector/device-room-selector.component';
import { DeviceDiscoverComponent } from './device-discover/device-discover.component';

// PAGES

// SERVICES
import { DeviceService } from './device.service';

// MODULES
import { DeviceRoutingModule } from './device-routing.module';
import { DeviceDiscoveredComponent } from './device-discovered/device-discovered.component';


@NgModule({
  declarations: [
    HomeDevicesComponent,
    RoomDevicesComponent,
    DeviceListComponent,
    DeviceDetailComponent,
    DeviceRoomSelectorComponent,
    DeviceDiscoverComponent,
    DeviceDiscoveredComponent,
  ],
  imports: [
    DeviceRoutingModule,
    CommonModule
  ],
  exports: [
    HomeDevicesComponent,
    RoomDevicesComponent,
    DeviceListComponent,
    DeviceDiscoverComponent
  ],
  providers: [DeviceService]
})
export class DeviceModule {}
