import { HuanJingLun } from './huanjinglun.coffee'
import {Tiangan} from '../basic/tiangan.coffee'
import {Dizhi} from '../basic/dizhi.coffee'
import util from 'util'
import {XinPaiBasic} from "/imports/Algorithm/xinpai/xinpaibasic"
import _ from 'lodash'
# 实神在大运流年出现，有力
# 

class DayunLiunian
	fortune:{}
	yearFortune:{}
	solution:1
	constructor:(@bazi,@paipan,@huanjinglun,@solution=1)->
		@XinPaiBasic=new XinPaiBasic()
		
		# solution 
		# 方案1 当大运空亡的时候，无论空亡的字是否是实神，都按照流年填实计算
		# 方案2 
		
		if @solution==1
			@buildDayunAndLiunianFortune()

	buildDayunAndLiunianFortune:()=>
		@buildDayunObjects()
		# _.map @fortune,(item,dayun)=>
		# 	console.log dayun
		# 	console.log item.shishen
		# 	console.log item.xushen
		# console.log util.inspect @fortune,false,10,true

	buildDayunObjects:()=>
		@fortune={}
		# console.log "共#{@paipan.length}个流年"
		_.map @paipan,(year)=>
			# { age: 81, year: 2068, zs: '帝旺', dayun: '壬寅', liunian: '戊子' },
			if not @fortune[year.dayun]
				@fortune[year.dayun]=
					name:year.dayun
					# tiangan:new Tiangan year.dayun[0]
					shishen:
						tiangan:[]
						dizhi:[]
					xushen:
						tiangan:[]
						dizhi:[]
					yinyang:if "甲丙戊庚壬".indexOf(year.dayun[0])>=0 then 1 else -1
					# dizhi:new Dizhi year.dayun[1]
					kongwang:if @bazi.kongwang.indexOf(year.dayun[1])>=0 then true else false
					startYear:year.year
					startAge:year.age
					endYear:year.year+9
					endAge:year.age+9
					years:[]

				if @bazi.str.indexOf(year.dayun[0])>=0
					@fortune[year.dayun].shishen.tiangan.push year.dayun[0]
				else
					@fortune[year.dayun].xushen.tiangan.push year.dayun[0]

				if @bazi.str.indexOf(year.dayun[1])>=0
					@fortune[year.dayun].shishen.dizhi.push year.dayun[1]
				else
					@fortune[year.dayun].xushen.dizhi.push year.dayun[1]
			@liunianFormatter year
			@fortune[year.dayun].years.push year
			@fortune[year.dayun][year.liunian]=year
		@yearFortune={}
		_.map @fortune,(item)=>
			@yearFortune[item.startYear]=item

	liunianFormatter:(year)=>
		year.shishen=
			tiangan:[]
			dizhi:[]
			tianganDayun:[]
			dizhiDayun:[]
		year.xushen=
			tiangan:[]
			dizhi:[]
			tianganDayun:[]
			dizhiDayun:[]
		year.yinyang=if "甲丙戊庚壬".indexOf(year.liunian[0])>=0 then 1 else -1
		year.dayunYinyang=if "甲丙戊庚壬".indexOf(year.dayun[0])>=0 then 1 else -1
		year.kongwang=if @bazi.kongwang.indexOf(year.liunian[1])>=0 then true else false
		year.dayunKongwang=if @bazi.kongwang.indexOf(year.dayun[1])>=0 then true else false
		
		if @bazi.str.indexOf(year.liunian[0])>=0
			year.shishen.tiangan.push year.liunian[0]
		else
			year.xushen.tiangan.push year.liunian[0]

		if @bazi.str.indexOf(year.liunian[1])>=0
			year.shishen.dizhi.push year.liunian[1]
		else
			year.xushen.dizhi.push year.liunian[1]

		if @bazi.str.indexOf(year.dayun[0])>=0
			year.shishen.tianganDayun.push year.dayun[0]
		else
			year.xushen.tianganDayun.push year.dayun[0]

		if @bazi.str.indexOf(year.dayun[1])>=0
			year.shishen.dizhiDayun.push year.dayun[1]
		else
			year.xushen.dizhiDayun.push year.dayun[1]
		
		@dayunLiunianEffectResult year
	
	
	###*
	 * 根据流年对象，判断大运流年的类型以及作用方式
	 * @param  {obejct} year 流年对象
	###
	dayunLiunianEffectResult:(year)=>
		# 大运流年空亡与填实
		
		# 大运流年之间的作用结果
		year.xushiEffectResult=@xushiEffectResult year
		# 命局中每个字的结果
		year.mingju=@dayunLiunianYuMingJu year
		# 环境论中每个六亲的结果
		year.liuqin=@dayunLiunianYuLiuqin year
		

	wangshuaiOfDayunAndLiunianTongxing:(element,type)=>
		if type=='tiangan'
			if @XinPaiBasic.tianganWangshuaiByDayunLiunian {name:element.element},{name:element.effectiveElement} then element.wangshuai=4 else element.wangshuai=-4
		else
			# 大运空亡，流年直接作用，有力
			if element.dayunKongwang
				element.position='liunian'
				element.type="同性作用，大运空亡"
				element.name='tongxing_dayunkongwang'
				element.kongwangElement=element.element
				element.element=element.effectiveElement
				element.wangshuai=4
		    # 大运不空亡，正常作用
			else	
				if @XinPaiBasic.dizhiWangshuaiByDayunLiunian {name:element.element},{name:element.effectiveElement} then element.wangshuai=4 else element.wangshuai=-4


	wangshuaiOfDayunAndLiunianYixing:(dayunElement,liunianElement,type)=>

		if type=='tiangan'
			wangshuaiFunc=@XinPaiBasic.tianganWangshuaiByDayunLiunian
		else
			wangshuaiFunc=@XinPaiBasic.dizhiWangshuaiByDayunLiunian
		
		# 大运的字，被流年作用，如果是流年生大运，那么大运是弱的，但不是非常弱
		if  wangshuaiFunc {name:dayunElement.element},{name:dayunElement.effectiveElement}
			dayunElement.wangshuai=-1
		# 大运的字，被流年作用，如果流年制大运，那么大运是旺的，但不是非常旺
		else
			dayunElement.wangshuai=1

		# 流年的字，被大运作用，如果是大运生流年，那么流年是弱的，但不是非常弱
		if  wangshuaiFunc {name:liunianElement.element},{name:liunianElement.effectiveElement}
			liunianElement.wangshuai=-1
		# 大运的字，被流年作用，如果流年制大运，那么大运是旺的，但不是非常旺
		else
			liunianElement.wangshuai=1

		# 地支作用中，大运空亡，按照地支填实
		if type=='dizhi' and dayunElement.dayunKongwang
			# 大运不作用
			dayunElement.effect=false

			dayunElement.type="异性作用，大运空亡"
			dayunElement.name="yixing_dayunkongwang"
			dayunElement.kongwangElement=dayunElement.element

			liunianElement.type=dayunElement.type
			liunianElement.name=dayunElement.name
			liunianElement.kongwangElement=dayunElement.kongwangElement

			dayunElement.element=dayunElement.effectiveElement
			liunianElement.wangshuai=4



	normalEffect:(year,type)=>
		result=[]
		# 实际上，分为同性作用和异性作用。
		# 同性力量大，异性力量小
		# 另外有大运流年出现的时候，实神有力。（但是比同性力小，比异性力大）
		# 这里用4、3、2、1、-1、-2、-3、-4来表示，
		# 4表示同性作用
		# 3表示实神大运流年出现，实神被同性增力或者减力
		# 2表示实神大运流年出现，实神被异性增力或者减力
		# 1表示异性作用


		# 大运空亡，不管流年是否空亡，按照流年旺并且是3

		# 大运流不空亡，不管流年是否空亡，也正常作用

		# 同性作用
		if year.dayunYinyang==year.yinyang
			element=
				type:'同性作用'
				name:"tongxing"
				effect:true
				position:'dayun'
				dayunKongwang:year.dayunKongwang
				liunianKongwang:year.kongwang
				element:if type=='tiangan' then year.dayun[0] else year.dayun[1]
				effectiveElement:if type=='tiangan' then year.liunian[0] else year.liunian[1]
			@wangshuaiOfDayunAndLiunianTongxing element,type
			result.push element
		# 异性作用
		else
			dayunElement=
				type:'异性作用'
				name:"yixing"
				effect:true
				position:'dayun'
				dayunKongwang:year.dayunKongwang
				liunianKongwang:year.kongwang
				element:if type=='tiangan' then year.dayun[0] else year.dayun[1]
				effectiveElement:if type=='tiangan' then year.liunian[0] else year.liunian[1]
			liunianElement=
				type:'异性作用'
				name:"yixing"
				effect:true
				position:'liunian'
				dayunKongwang:year.dayunKongwang
				liunianKongwang:year.kongwang
				element:if type=='tiangan' then year.liunian[0] else year.liunian[1]
				effectiveElement:if type=='tiangan' then year.dayun[0] else year.dayun[1]
			
			@wangshuaiOfDayunAndLiunianYixing dayunElement,liunianElement,type
			if dayunElement.effect then result.push dayunElement
			if liunianElement.effect then result.push liunianElement
		
		result


	xuxuEffect:(year,type)=>
		# 虚神之间作用
		# 1.大运流年同性作用时,大运为主,流年为辅,流年不直接与命局中的字发生作用.流年使大运之字增力或减力,增力或减力的大运(结果)再与命局中的字分别发生作用,从而决定吉凶
		@normalEffect year,type


	shiEffectedByXu:(year,type)=>
		if type=="tiangan"
			effectFunc=@XinPaiBasic.tianganWangshuaiByDayunLiunian
			if year.shishen.tiangan.length
				shishen=year.shishen.tiangan[0]
				xushen=year.xushen.tianganDayun[0]
				position="liunian"
				name="dayun_xu_liunian_shi"
				etype="大运虚神，流年实神"
			else if year.shishen.tianganDayun.length
				shishen=year.shishen.tianganDayun[0]
				xushen=year.xushen.tiangan[0]
				position="dayun"
				name="dayun_shi_liunian_xu"
				etype="大运实神，流年虚神"
		else
			effectFunc=@XinPaiBasic.dizhiWangshuaiByDayunLiunian
			if year.shishen.dizhi.length
				shishen=year.shishen.dizhi[0]
				xushen=year.xushen.dizhiDayun[0]
				position="liunian"
				name="dayun_xu_liunian_shi"
				etype="大运虚神，流年实神"
			else if year.shishen.dizhiDayun.length
				shishen=year.shishen.dizhiDayun[0]
				xushen=year.xushen.dizhi[0]
				position="dayun"
				name="dayun_shi_liunian_xu"
				etype="大运实神，流年虚神"
		
		wangruo=effectFunc {name:shishen},{name:xushen}
		wangshuai=0
		if year.dayunYinyang==year.yinyang 
			if wangruo then wangshuai=3 else wangshuai=-3
			etype+='，同性作用'
			name+='_tongxing'
		else
			if wangruo then wangshuai=2 else wangshuai=-2
			etype+='，异性作用'
			name+='_yixing'
		result=
			shishen:shishen
			xushen:xushen
			dayunKongwang:year.dayunKongwang
			effect:true
			effectiveElement:xushen
			element:shishen
			liunianKongwang:year.kongwang
			name:name
			type:etype
			position:position
			wangruo:wangruo
			wangshuai:wangshuai

	xushiEffect:(year,type)=>
		# 2.大运流年异性作用时,大运流年不分主次,分别与命局中的同性字发生作用.异性的大运流年间作用力小,但不容忽视,还是要首先发挥作用.

		# 虚实都有
		# 大运流年虚实作用时,按照实神首先被作用论,实神被虚神增力或减力断一个结果,断出这个结果后,再按照正常的大运流年作用关系再断另一个结果
		# a.大运流年虚实同性作用时,实神首先被作用断一个结果,然后再按照大运为主,流年为辅,流年通过大运作用于命局的原则与局中其它字发生作用,以决断吉凶.
		# b.大运流年异性作用时,同样是实神首先被作用,实神被虚神增力或减力后,断一个结果.然后大运流年不分主次分别与命局中的同性字发生作用.异性的大运流年间首先发生作用
		
		# 方案1，当大运地支空亡的时候，无论虚实，直接用流年地支填实作用
		if @solution==1
			# 如果大运地支空亡，不考虑虚实，直接用流年填实作用，这个作用方法，与虚虚作用是一致的
			if not (type=='dizhi' and year.dayunKongwang)
				# 如果大运不空亡，大运是实神，流年正常先与之作用
				# 如果大运不空亡，大运是虚神，流年是实神，那么大运先与流年作用
				# 总之，先虚神与实神作用，如果流年空亡，在最外面再判断
				xushiEffectResult=@shiEffectedByXu year,type

			normalResult=@normalEffect year,type

			result=[]
			if xushiEffectResult then result.push xushiEffectResult
			_.map normalResult,(item)=>result.push item
			
			result
		# 方案2，依旧按照实神先被虚神作用
		# 作用时，如果实神空亡，
		else if @solution==2
			undefined	

	shishiEffect:(year,type)=>
		# 实实作用
		# c.实实作用,吉凶皆有.大运流年为两个实神作用时,先把流年看作有力断一个结果,然后再把流年无力看作一个结果,这两个结果是相反的,在同一流年的不同月份上出现,最终应吉还是应凶,看大运而定.大运吉,先凶后吉;大运凶,先吉后凶

		# 大运实神，流年实神
		# 1 大运空亡
		# 2 流年空亡
		# 3 大运流年都空亡
		
		# 大运实神，流年虚神
		# 1 大运空亡
		# 2 流年空亡
		# 3 大运流年都空亡
		
		# 大运虚神，流年实神
		# 1 大运空亡
		# 2 流年空亡
		# 3 大运流年都空亡

		# 如果大运空亡，则这个实神不存在，需要用流年填实
		# #无论流年是否空亡，则就一个流年实神存在，按照实神有力断一个，按照实神无力断一个
		# 
		# 如果大运不空亡
		# #大运旺是一个结果，流年一个有力，一个无力

		# 所以流年一定要断一个有力，一个无力，大运只要不空亡一定断一个有力
		dayunIsEffective=(!year.dayunKongwang) #and (year.dayun[if type=='tiangan' then 0 else 1]!=year.liunian[if type=='tiangan' then 0 else 1])
		dayunEffect=
			shishen:[year.dayun[if type=='tiangan' then 0 else 1],year.liunian[if type=='tiangan' then 0 else 1]]
			dayunKongwang:year.dayunKongwang
			effect:dayunIsEffective
			element:year.dayun[if type=='tiangan' then 0 else 1]
			liunianKongwang:year.kongwang
			name:'shi_shi_dayun'+if year.dayunKongwang then '_kongwang' else ''
			type:'实实作用，大运有力'+if year.dayunKongwang then '，大运空亡' else ''
			position:'dayun'
			wangshuai:4
		liunianLiEffect=
			shishen:[year.dayun[if type=='tiangan' then 0 else 1],year.liunian[if type=='tiangan' then 0 else 1]]
			dayunKongwang:year.dayunKongwang
			effect:true
			element:year.dayun[if type=='tiangan' then 0 else 1]
			liunianKongwang:year.kongwang
			name:'shi_shi_liunian_strong'
			type:'实实作用，流年有力'
			position:'liunian'
			wangshuai:3
		liunianWuLiEffect=
			shishen:[year.dayun[if type=='tiangan' then 0 else 1],year.liunian[if type=='tiangan' then 0 else 1]]
			dayunKongwang:year.dayunKongwang
			effect:not year.dayunKongwang
			element:year.dayun[if type=='tiangan' then 0 else 1]
			liunianKongwang:year.kongwang
			name:'shi_shi_liunian_weak'
			type:'实实作用，流年无力'
			position:'liunian'
			wangshuai:-3
		result=[]
		if dayunEffect.effect then result.push dayunEffect
		result.push liunianLiEffect
		result.push liunianWuLiEffect
		result
	###*
	 * 根据大运流年，计算天干或者地支的作用结果
	 * @param  {object} year 大运流年对象
	 * @param  {string} type tiangan | dizhi
	 * @return {array}      作用结果，是一个数组，包括实神存在和不存在时的作用结果
	###
	calculateXushiEffect:(year,type)=>
		count=0
		if year.shishen[type].length==1 then count+=1
		if year.shishen[type+"Dayun"].length==1 then count+=1
		# 虚虚作用
		if count==0
			{
				result:@xuxuEffect year,type
				type:'虚神与虚神作用'
				name:"xuxu"
			}
		# 虚实作用
		else if count==1
			{
				result:@xushiEffect year,type
				type:"虚神与实神作用"
				name:"xushi"
			}
		# 实实作用
		else if count==2
			{
				result:@shishiEffect year,type
				type:"实神与实神作用"
				name:"shishi"
			}

	###*
	 * 获取一个大运流年的虚实作用与旺弱结果
	 * @param  {object} year 大运流年对象
	 * @return {object}      结果对象
	###
	xushiEffectResult:(year)=>
		result=
			tiangan:@calculateXushiEffect year,'tiangan'
			dizhi:@calculateXushiEffect year,'dizhi'

	kongwangType:()=>
		# 命局中空亡的字，要用大运填实再去作用
		# 如果大运地支空亡，用流年地支填实
		# 如果流年地支空亡，那么用流年地支填实后，再反断
		# 本质是，空了的字，就没了……
		# 

	mingJuElementEffectByDayunLiunian:(element,dylnEffect,year)=>
		elementResult=
			name:element
			toEffect:element
		if '甲丙戊庚壬'.indexOf(element)>=0
			type='tiangan'
			elementResult.yinyang=1
		else if "乙丁己辛癸".indexOf(element)>=0
			type='tiangan'
			elementResult.yinyang=-1
		else if "子寅辰午申戌".indexOf(element)>=0
			type='dizhi'
			elementResult.yinyang=1
			elementResult.elementKongwang=if @bazi.kongwang.indexOf(element)>=0 then true else false
		else
			type='dizhi'
			elementResult.yinyang=-1
			elementResult.elementKongwang=if @bazi.kongwang.indexOf(element)>=0 then true else false
		
		if elementResult.elementKongwang
			if year.dayunKongwang
				elementResult.toEffect=year.liunian[1]
			else
				elementResult.toEffect=year.dayun[1]
		
		elementResult.result=[]
		
		effectFunc=if type=='tiangan' then @XinPaiBasic.tianganWangshuaiByDayunLiunian else @XinPaiBasic.dizhiWangshuaiByDayunLiunian

		# 大运先作用一个结果，如果空亡，把空亡写出来
		dayunElement=if type=='tiangan' then year.dayun[0] else year.dayun[1]
		dayunEffectResult=
			type:'大运的作用'
			name:"dayun_effect"
			element:dayunElement
			effectStrong:if elementResult.yinyang==year.dayunYinyang then 1 else -1
			kongwang:if year.dayunKongwang and type=='dizhi' then 1 else -1
			wangshuai:if effectFunc {name:elementResult.toEffect},{name:dayunElement} then 1 else -1
		dayunEffectResult.score=(-1*dayunEffectResult.kongwang)*dayunEffectResult.wangshuai
		elementResult.result.push dayunEffectResult
		# 大运流年作用后再与之作用的结果
		_.map dylnEffect,(effect,key)=>
			effectYinyang=if effect.position=='liunian' then year.yinyang else year.dayunYinyang
			elementEffectResult=_.cloneDeep effect
			elementEffectResult.effectStrong=if elementResult.yinyang==effectYinyang then 1 else -1
			elementEffectResult.effectWangshuai=if effectFunc {name:elementResult.toEffect},{name:effect.element} then 1 else -1
			# 遇到流年空亡之后，作用结果x-1
			if year.kongwang and type=='dizhi' and effect.position=='liunian' then elementEffectResult.liunianKongwang=1 else elementEffectResult.liunianKongwang=-1
			elementEffectResult.score=(-1*elementEffectResult.liunianKongwang)*elementEffectResult.effectWangshuai*effect.wangshuai
			elementResult.result.push elementEffectResult
		elementResult
	
	dayunLiunianYuMingJu:(year)=>
		xushiEffectResult=year.xushiEffectResult
		result=
			RiGan:@mingJuElementEffectByDayunLiunian @bazi.RiGan.name,xushiEffectResult.tiangan.result,year
			RiZhi:@mingJuElementEffectByDayunLiunian @bazi.RiZhi.name,xushiEffectResult.dizhi.result,year
			ShiGan:@mingJuElementEffectByDayunLiunian @bazi.ShiGan.name,xushiEffectResult.tiangan.result,year
			ShiZhi:@mingJuElementEffectByDayunLiunian @bazi.ShiZhi.name,xushiEffectResult.dizhi.result,year
			YueGan:@mingJuElementEffectByDayunLiunian @bazi.YueGan.name,xushiEffectResult.tiangan.result,year
			YueZhi:@mingJuElementEffectByDayunLiunian @bazi.YueZhi.name,xushiEffectResult.dizhi.result,year
			NianGan:@mingJuElementEffectByDayunLiunian @bazi.NianGan.name,xushiEffectResult.tiangan.result,year
			NianZhi:@mingJuElementEffectByDayunLiunian @bazi.NianZhi.name,xushiEffectResult.dizhi.result,year


	liuqinEnvEffect:(liuqin,mingju)=>
		neiwai=['nei','wai']
		fs=['family','social']
		_.map neiwai,(element)=>
			# console.log liuqin
			# console.log liuqin.env[element].positionName
			# console.log mingju[liuqin.env[element].positionName]
			liuqin.env[element].wangshuai=_.cloneDeep mingju[liuqin.env[element].positionName]
			# console.log liuqin.env[element].wangshuai
			_.map fs,(e)=>
				liuqin.env[element][e].wangshuai=_.cloneDeep mingju[liuqin.env[element][e].positionName]
		liuqin
	
	dayunLiunianYuLiuqin:(year)=>

		mingju=year.mingju
		result={}
		_.map @huanjinglun.liuqin,(liuqin,name)=>
			result[name]=_.cloneDeep @liuqinEnvEffect liuqin,mingju

		result

exports.DayunLiunian=DayunLiunian




