import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { HumeComponent } from './hume.component';
import { HumeListComponent } from './hume-list/hume-list.component';

// SERVICES
import { HumeService } from './hume.service';

// MODULES
import { HumeRoutingModule } from './hume-routing.module';

@NgModule({
  declarations: [
    HumeComponent,
    HumeListComponent
  ],
  imports: [
    HumeRoutingModule,
    CommonModule
  ],
  exports: [

  ],
  providers: [HumeService]
})
export class HumeModule {}
