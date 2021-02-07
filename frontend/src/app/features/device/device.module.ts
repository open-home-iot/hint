import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { DeviceListComponent } from './device-list/device-list.component';
import { DeviceDetailComponent } from './device-detail/device-detail.component';
import { DeviceConfigurationComponent } from './device-configuration/device-configuration.component';
import { DeviceOverviewComponent } from './pages/device-overview/device-overview.component';

// SERVICES
import { DeviceService } from './device.service';

// MODULES
import { DeviceRoutingModule } from './device-routing.module';

@NgModule({
  declarations: [
    DeviceListComponent,
    DeviceDetailComponent,
    DeviceConfigurationComponent,
    DeviceOverviewComponent
  ],
  imports: [
    DeviceRoutingModule,
    CommonModule
  ],
  exports: [
    DeviceListComponent
  ],
  providers: [DeviceService]
})
export class DeviceModule {}
