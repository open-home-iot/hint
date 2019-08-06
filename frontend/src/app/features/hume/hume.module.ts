import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { HumeListComponent } from './hume-list/hume-list.component';
import { HumeDetailComponent } from './hume-detail/hume-detail.component';
import { HumeOverviewComponent } from './pages/hume-overview/hume-overview.component';

// SERVICES
import { HumeService } from './hume.service';

// MODULES
import { HumeRoutingModule } from './hume-routing.module';

@NgModule({
  declarations: [
    HumeListComponent,
    HumeDetailComponent,
    HumeOverviewComponent
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
