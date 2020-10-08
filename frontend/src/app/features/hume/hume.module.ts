import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS

// PAGES
import { HumeOverviewComponent } from './pages/hume-overview/hume-overview.component';

// SERVICES
import { HumeService } from './hume.service';

// MODULES
import { HumeRoutingModule } from './hume-routing.module';

@NgModule({
  declarations: [
    HumeOverviewComponent
  ],
  imports: [
    HumeRoutingModule,
    CommonModule
  ],
  exports: [
    HumeOverviewComponent
  ],
  providers: [HumeService]
})
export class HumeModule {}
