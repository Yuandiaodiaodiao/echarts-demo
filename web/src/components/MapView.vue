<template>
  <el-container style="height: 100% ">
    <el-header>Header</el-header>
    <el-container>

      <el-aside width="300px">
        <el-row>
          <el-col :span="6">
            热度权重:
          </el-col>
          <el-col :span="18">
            <el-select v-model="value1" placeholder="请选择">
              <el-option
                v-for="item in heatvalue"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6">
            显示粒度:
          </el-col>
          <el-col :span="18">
            <el-switch
              v-model="value2"
              active-color="#13ce66"
              inactive-color="#13ce66"
              active-text="食品"
              inactive-text="店铺">
            </el-switch>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="8" style="font-size: small">
            店铺名称筛选:
          </el-col>
          <el-col :span="16">
            <el-input v-model="value3"></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="8" style="font-size: small">
            食品名称筛选:
          </el-col>
          <el-col :span="16">
            <el-input v-model="value4"></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="8" style="font-size: small">
            地点筛选:
          </el-col>
          <el-col :span="16">
            <el-input v-model="value5"></el-input>
          </el-col>
        </el-row>
        <el-button type="primary" @click="query">查询</el-button>
        <el-button type="primary" @click="dialogTableVisible = true" v-if="value1!=='无'">查看top10</el-button>
        <el-row>
          <el-col :span="12">
            <el-button type="primary" @click="querynum">导出</el-button>
          </el-col>
          <el-col :span="6">
            导出数量:
          </el-col>
          <el-col :span="6">
            <el-input v-model="topN" placeholder="top(n)"></el-input>
          </el-col>
        </el-row>
        <el-dialog title="收货地址" :visible.sync="dialogTableVisible" width="80%">
          <el-table :data="gridData">
            <el-table-column property="name" label="店铺名称" width="100"></el-table-column>
            <el-table-column property="food_name" label="食品名称" v-if="value2==true " width="100"></el-table-column>
            <el-table-column property="month_sales" label="月销量" width="100"></el-table-column>
            <el-table-column property="price" label="价格" width="100"></el-table-column>
            <el-table-column property="rating" label="评分" width="100"></el-table-column>
            <el-table-column property="month_money" label="月销售额" width="100"></el-table-column>
            <el-table-column property="address" label="店铺地址" width="100"></el-table-column>
          </el-table>
        </el-dialog>
      </el-aside>

      <el-main>
        <el-card style="width: 100%;height: 100%" :body-style="{padding:'20px',height:'100%',width:'100%'}">
          <div id="container" style=" width:  95%; height: 100%; "></div>
        </el-card>
      </el-main>
    </el-container>
  </el-container>

</template>

<script>
  let BMap = require('echarts/extension/bmap/bmap')
  import consts from '@/consts/consts'
  import XLSX from 'xlsx'

  export default {
    name: "MapView",
    data() {
      return {
        topN: 10,
        gridData: [],
        dialogTableVisible: false,
        heatvalue: consts.heatvalue,
        points: [120.13066322374, 30.240018034923, 1],
        value1: "无",
        value2: true,
        value3: "",
        value4: "",
        value5: "",
        myChart: undefined
      }
    },
    mounted() {
      this.myChart =
        this.$echarts.init(document.getElementById("container"));
      this.drawChart();


    },
    computed: {},
    methods: {
      async querynum() {
        this.$message('正在查询 请稍等');
        console.log('querynum' + this.topN)

        let res = await this.axios.post(this.config_const.api_url, JSON.stringify({
          'op': 'query',
          'heat': this.value1,
          'type': this.value2,
          'shopname': this.value3,
          'foodname': this.value4,
          'address': this.value5,
          'num': this.topN
        }))
        let rawdata = res.data.top10
        let head = [
          'food_id', 'food_name', 'price', 'rating', 'month_sales', 'rating_count', 'statisfy_count', 'statisfy_rate', 'min_purchase', 'category_id', 'id', 'name', 'address', 'latitude', 'longitude', 'month_money'
        ]
        let headshow = [
          '食物id', '食物name', '价格', '食物rating', '月销量(个)', 'rating数量', 'statisfy_count', 'statisfy_rate', 'min_purchase', '分类id', '店铺id', '店铺名称', '地址', 'latitude', 'longitude', '月销量(元)'
        ]
        let ws_data = [
          headshow
        ]
        for (let x in rawdata) {
          let arr = []
          for (let y in head) {
            arr.push((rawdata[x][head[y]]||'')+'')
          }
          ws_data.push(arr)
        }
        let ws = XLSX.utils.aoa_to_sheet(ws_data);
        let new_workbook = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(new_workbook, ws, 'sheet1')
        let sheet=new_workbook.Sheets['sheet1']
        let wd=[]
        for(let i=0;i<=1;i+=1){
          wd.push({wpx:130})
        }
        for(let i=2;i<=8;i+=1){
          wd.push({wpx:40})
        }
        for(let i=9;i<=14;i+=1){
          wd.push({wpx:130})
        }
        sheet['!cols']=wd
        let dat = new Date()
        XLSX.writeFile(new_workbook, 'output'  + '.xlsx')
        this.$message({
          message: '查询完成',
          type: 'success'
        });
      },
      async query() {
        this.$message('正在查询 请稍等');
        let res = await this.axios.post(this.config_const.api_url, JSON.stringify({
          'op': 'query',
          'heat': this.value1,
          'type': this.value2,
          'shopname': this.value3,
          'foodname': this.value4,
          'address': this.value5,
          'num': -1
        }))
        this.points = res.data.ans

        this.myChart.setOption({visualMap: {min: 0, max: res.data.midd * 10, range: [0, res.data.midd * 10]}}); // 设置了 range
        let option = this.myChart.getOption()
        option.series[0].data = this.points
        this.myChart.setOption(option);
        // console.log(this.myChart.getOption())
        this.gridData = res.data.top10
        this.$message({
          message: '查询完成',
          type: 'success'
        });
      },
      drawChart() {
        this.myChart.setOption({
          animation: false,
          bmap: {
            center: [110.13066322374, 30.240018034923],
            zoom: 6,
            roam: true
          },
          visualMap: {
            show: true,
            top: 'top',
            min: 0,
            max: 10,
            range: [0, 10],
            seriesIndex: 0,
            calculable: true,
            inRange: {
              color: consts.color1
            }
          },
          series: [{
            type: 'heatmap',
            coordinateSystem: 'bmap',
            data: this.points,
            large: true,
            progressive: 4000,
            pointSize: 10,
            blurSize: 4
          }]
        });

        var bmap = this.myChart.getModel().getComponent('bmap').getBMap();
        bmap.addControl(new BMap.MapTypeControl());

      }
    }
  }


</script>

<style scoped>
  .el-header, .el-footer {
    background-color: #f3f3f3;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #f9f9f9;
    color: #333;
    text-align: center;
    line-height: 50px;
  }

  .el-main {
    background-color: #FFFFFF;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
