import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

// COMPONENTS
import { HumeFindComponent } from './hume-status/hume-find/hume-find.component';
import { HumeListComponent } from './hume-list/hume-list.component';
import { HumeStatusComponent } from './hume-status/hume-status.component';

// PAGES

// SERVICES
import { HumeService } from './hume.service';

// MODULES
import { HumeRoutingModule } from './hume-routing.module';
import { DeviceModule } from '../device/device.module';

@NgModule({
  declarations: [
    HumeFindComponent,
    HumeListComponent,
    HumeStatusComponent
  ],
  imports: [
    HumeRoutingModule,
    CommonModule,
    ReactiveFormsModule,
    DeviceModule
  ],
  exports: [
    HumeFindComponent,
    HumeListComponent,
    HumeStatusComponent
  ],
  providers: [HumeService]
})
export class HumeModule {}
