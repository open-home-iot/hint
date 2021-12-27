import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

// COMPONENTS
import { HumeFindComponent } from './hume-status/hume-find/hume-find.component';
import { HumeStatusComponent } from './hume-status/hume-status.component';
import { HumeDetailComponent } from './hume-detail/hume-detail.component';

// PAGES

// SERVICES
import { HumeService } from './hume.service';

// MODULES
import { HumeRoutingModule } from './hume-routing.module';
import { DeviceModule } from '../device/device.module';

@NgModule({
  declarations: [
    HumeFindComponent,
    HumeStatusComponent,
    HumeDetailComponent
  ],
  imports: [
    HumeRoutingModule,
    CommonModule,
    ReactiveFormsModule,
    DeviceModule
  ],
  exports: [
    HumeFindComponent,
    HumeStatusComponent,
    HumeDetailComponent
  ],
  providers: [HumeService]
})
export class HumeModule {}
