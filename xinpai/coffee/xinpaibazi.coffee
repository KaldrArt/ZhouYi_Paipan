import { PaipanFinder } from '../basic/paipanFinder.coffee'
import { XinPaiGeju } from './geju.coffee'
import { Bazi } from '../basic/bazi.coffee'
import {BaiShenLun} from './baishenlun.coffee'
import {HuanJingLun} from './huanjinglun.coffee'
import { DayunLiunian} from './dayunliunian.coffee'

class XinPaiBaZi 
	constructor:(@date,@sex)->
		@setSex(@sex)
		@Bazi={}
		@BaziPaiPan={}
		@XinPaiGeju={}
		@BaiShenLun={}
		@HuanJingLun={}
		@DayunLiunian={}
		# 1.排盘
		@paipan()
		
		# 2.格局用神
		@buildGeju()
		
		# 3.百神论
		@buildBaishen()

		# 4.环境论
		@buildHuanjing()

		# 5.大运流年
		@buildDayunLiunian()
	
	setSex:(sex)=>
		if [1,'男','乾造','乾','1'].indexOf(sex)>=0
			@sex="乾"
		else
			@sex="坤"

	
	paipan:()=>
		if not @PaipanFinder then @PaipanFinder=new PaipanFinder @date,@sex
		@BaziPaiPan=@PaipanFinder.findBaziFromDb()
		@Bazi = new Bazi @BaziPaiPan.name,@sex
		
	buildGeju:()=>
		@XinPaiGeju=new XinPaiGeju @Bazi

	buildBaishen:()=>
		@BaiShenLun=new BaiShenLun @Bazi,@XinPaiGeju
	
	buildHuanjing:()=>
		@HuanJingLun=new HuanJingLun @Bazi,@BaiShenLun
	
	buildDayunLiunian:()=>
		@DayunLiunian=new DayunLiunian @Bazi,@BaziPaiPan.fortune,@HuanJingLun
		
exports.XinPaiBaZi=XinPaiBaZi