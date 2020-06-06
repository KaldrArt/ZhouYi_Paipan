import {MuKuLun} from './mukulun.coffee'


class XinPaiBasic
	dizhi:'子丑寅卯辰巳午未申酉戌亥'
	dizhiWuxing:"水土木木土火火土金金土水"
	wuxing:"水木火土金"
	tiangan:"甲乙丙丁戊己庚辛壬癸"
	tianganWuxing:"木木火火土土金金水水"

	constructor:()->
		@MuKuLun=new MuKuLun()
	###*
	 * 天干之间的旺衰
	 * 判断的是第二个对第一个的影响，比如第二个是丁，第一个是乙，那么结果是false
	 * @param  {object} tiangan1Ob 天干对象
	 * @param  {object} tiangan2Ob 天干对象
	 * @return {boolean}            true旺，false衰
	###
	tianganWangshuai:(tiangan1Ob,tiangan2Ob)=>
		tiangan1wuxingindex=@wuxing.indexOf @tianganWuxing[@tiangan.indexOf tiangan1Ob.name]
		tiangan2wuxingindex=@wuxing.indexOf @tianganWuxing[@tiangan.indexOf tiangan2Ob.name]
		if ((tiangan1wuxingindex+3)%5==tiangan2wuxingindex) or ((tiangan2wuxingindex+3)%5==tiangan1wuxingindex) or ((tiangan1wuxingindex+1)%5==tiangan2wuxingindex) then false else true


	###*
	 * 日主生于某月的旺弱
	 * @param  {object} tiangan 天干
	 * @param  {object} dizhi   地支
	 * @return {boolean}         是否旺
	###
	rizhuYuelingWangshuai:(tiangan,dizhi)=>
		# 日主生于辰戌丑未月
		if ["辰","戌","丑","未"].indexOf(dizhi.name)>=0
			@MuKuLun.RiGanWangshuaiYuYueling tiangan,dizhi
		else
			if @wangshuai tiangan,dizhi then 1 else -1

	rizhuNianLingWangshuai:(tiangan,dizhi)=>
		# 日主生于辰戌丑未月
		if ["辰","戌","丑","未"].indexOf(dizhi.name)>=0
			@MuKuLun.RiGanWangshuaiYuNianling tiangan,dizhi
		else
			@wangshuai tiangan,dizhi
	###*
	 * 根据墓库论来判断旺衰
	 * @param  {object}  tiangan        天干对象
	 * @param  {object}  dizhi          地支对象
	 * @param  {Boolean} isYueGan=false 是否是月干
	 * @return {boolean}                 true旺，false弱
	###
	wangshuaiWithMukuLun:(tiangan,dizhi,isYueGan=false)=>
		if "辰戌丑未".indexOf(dizhi.name)>=0
			if isYueGan
				@MuKuLun.yuezhuWangShuai tiangan,dizhi
			else
				@MuKuLun.otherTongzhuWangshuai tiangan,dizhi
		else
			@wangshuai tiangan,dizhi
	###*
	 * 同柱天干与地支的关系
	 * @param  {object} tiangan 天干对象
	 * @param  {object} dizhi   地支对象
	 * @return {boolean}         是否旺
	###
	wangshuai:(tiangan,dizhi)=>
		tianganWuxingIndex=@wuxing.indexOf @tianganWuxing[@tiangan.indexOf tiangan.name]
		dizhiWuxingIndex=@wuxing.indexOf @dizhiWuxing[@dizhi.indexOf dizhi.name]
		# 克、耗、泄，则弱
		if ((tianganWuxingIndex+3)%5==dizhiWuxingIndex) or ((dizhiWuxingIndex+3)%5==tianganWuxingIndex) or ((tianganWuxingIndex+1)%5==dizhiWuxingIndex) then false else true
	
	tianganBeiZhi:(tianganOb,dizhiOb)=>
		not @wangshuai tianganOb,dizhiOb
	
	tianganBeiFu:()=>
		@wangshuai tianganOb,dizhiOb
	
	gen:(tiangan,dizhi)=>

	###*
	 * 被克
	 * @param  {number} dizhi1 五行序号
	 * @param  {number} dizhi2 五行序号
	 * @return {boolean}        是否被制
	###
	dizhiBeiKe:(dizhi1,dizhi2,dizhi1Ob,dizhi2Ob)=>
		# 地支中，辰丑土不克亥子水
		if [0,11].indexOf(@dizhi.indexOf dizhi1Ob.name)>=0 and [1,4].indexOf(@dizhi.indexOf dizhi2Ob.name)>=0 then false
		else if [8,9].indexOf(@dizhi.indexOf dizhi1Ob.name)>=0 and [7,10].indexOf(@dizhi.indexOf dizhi2Ob.name)>=0 then true
		# 其他根据五行生克制化判断
		else if (dizhi1+3)%5 == dizhi2 then true else false

	###*
	 * 被泄
	 * @param  {number} dizhi1 地支序号
	 * @param  {number} dizhi2 地支序号
	 * @return {boolean}        是否被制
	###
	dizhiBeiXie:(dizhi1,dizhi2,dizhi1Ob,dizhi2Ob)=>
		# 地支中未戌土，不泄巳午火
		if [5,6].indexOf(@dizhi.indexOf dizhi1Ob.name)>=0 and [7,10].indexOf(@dizhi.indexOf dizhi2Ob.name)>=0 then false
		# 地支中申酉金，不泄未戌土
		else if [7,10].indexOf(@dizhi.indexOf dizhi1Ob.name)>=0 and [8,9].indexOf(@dizhi.indexOf dizhi2Ob.name)>=0 then false
		# 其他根据五行生克制化判断
		else if (dizhi1+1)%5 == dizhi2 then true else false
	
	###*
	 * 地支被大运流年合，但是地支减力
	 * @param  {object} dizhi1 地支1对象
	 * @param  {object} dizhi2 地支2对象
	 * @return {boolean}       true 减力，false 不减力
	###
	dizhiBeiDayunliunianHeJianli:(dizhi1,dizhi2)=>
		if dizhi1<=6 and dizhi1>=1 and (dizhi2==0 or dizhi2>=7)
			if (6-dizhi1)%12+(12-dizhi2)%12==5
				if [2,7,9].indexOf(dizhi1)>=0 then false else true
			else
				false
		else if dizhi2<=6 and dizhi2>=1 and (dizhi1==0 or dizhi1>=7)
			if (6-dizhi2)%12+(12-dizhi1)%12==5
				if [2,7,9].indexOf(dizhi1)>=0 then false else true
			else
				false
		else
			false
	###*
	 * 地支被大运流年合，但是地支增力	
	 * @param  {object} dizhi1 地支1对象
	 * @param  {object} dizhi2 地支2对象
	 * @return {boolean}       true 增力, false 不增力
	###
	dizhiBeiDayunliunianHeZengli:(dizhi1,dizhi2)=>
		if dizhi1<=6 and dizhi1>=1 and (dizhi2==0 or dizhi2>=7)
			if (6-dizhi1)%12+(12-dizhi2)%12==5
				if [2,7,9].indexOf(dizhi1)>=0 then true else false
			else
				false
		else if dizhi2<=6 and dizhi2>=1 and (dizhi1==0 or dizhi1>=7)
			if (6-dizhi2)%12+(12-dizhi1)%12==5
				if [2,7,9].indexOf(dizhi1)>=0 then true else false
			else
				false
		else
			false
	###*
	 * 地址被合，并且减力
	 * 寅、酉、未在合的时候，增力，其他减力
	 * @param  {[type]} dizhi1 [description]
	 * @param  {[type]} dizhi2 [description]
	 * @return {[type]}        [description]
	###
	dizhiBeiHe:(dizhi1,dizhi2)=>
		if dizhi1<=6 and dizhi1>=1 and (dizhi2==0 or dizhi2>=7)
			if (6-dizhi1)%12+(12-dizhi2)%12==5
				if [2,7,9].indexOf(dizhi1)>=0 then false else true
			else
				false
		else if dizhi2<=6 and dizhi2>=1 and (dizhi1==0 or dizhi1>=7)
			if (6-dizhi2)%12+(12-dizhi1)%12==5
				if [2,7,9].indexOf(dizhi1)>=0 then false else true
			else
				false
		else
			false
			
	###*
	 * 地支被冲
	 * @param  {number} dizhi1 地支序号
	 * @param  {number} dizhi2 地支序号
	 * @return {boolean}        是否被制
	###
	dizhiBeiChong:(dizhi1,dizhi2)=>
		if (dizhi1+6)%12 == dizhi2 then true else false
	
	###*
	 * 是否被刑
	 * @param  {number} dizhi1 地支序号
	 * @param  {number} dizhi2 地支序号
	 * @return {boolean}        是否被制
	###
	dizhiBeiXing:(dizhi1,dizhi2)=>
		if (dizhi1==1 and dizhi2==10 ) or (dizhi1==10 and dizhi2==1) then true else false
	
	###*
	 * 地支之间的关系
	 * 地支2对地支1的关系
	 * @param  {object} dizhi1 地支1对象
	 * @param  {object} dizhi2 地支2对象
	 * @return {boolean}        旺true
	###
	dizhiWangshuai:(dizhi1,dizhi2)=>
		not @dizhiBeiZhi dizhi1,dizhi2
	
	tianganWangshuaiByDayunLiunian:(tiangan1,tiangan2)=>
		result=@tianganWangshuai tiangan1,tiangan2
		tiangan1Index=@tiangan.indexOf tiangan1.name
		tiangan2Index=@tiangan.indexOf tiangan2.name
		if tiangan1Index%2!=tiangan2Index%2 then result=!result
		result

	dizhiWangshuaiByDayunLiunian:(dizhi1,dizhi2)=>
		dizhi1Index=@dizhi.indexOf dizhi1.name
		dizhi2Index=@dizhi.indexOf dizhi2.name
		dizhi1Wuxing=@wuxing.indexOf @dizhiWuxing[@dizhi.indexOf dizhi1.name]
		dizhi2Wuxing=@wuxing.indexOf @dizhiWuxing[@dizhi.indexOf dizhi2.name]
		# 地支2 冲 地支1
		if @dizhiBeiChong dizhi1Index,dizhi2Index
			result=false
		# 地支2 刑 地支1
		else if @dizhiBeiXing dizhi1Index,dizhi2Index
			result=false
		# 地支2 合 地支1，并且地支1增力
		else if @dizhiBeiDayunliunianHeZengli dizhi1Index,dizhi2Index
			result=true
		# 地支2 合 地支1，并且地支1减力	
		else if @dizhiBeiDayunliunianHeJianli dizhi1Index,dizhi2Index
			result=false
		else 
			# 地支2 克 地支1
			if @dizhiBeiKe dizhi1Wuxing,dizhi2Wuxing,dizhi1,dizhi2
				result=false
			# 地支2 泄 地支1
			else if @dizhiBeiXie dizhi1Wuxing,dizhi2Wuxing,dizhi1,dizhi2
				result=false
			
			# 地支2 耗 地支1
			else if @dizhiBeiKe dizhi2Wuxing,dizhi1Wuxing,dizhi2,dizhi1
				result=false
			else
				result=true
			# 如果阴阳不同，结果反过来
			if dizhi1Index%2 != dizhi2Index%2 then result=!result
		result


	###*
	 * 地支是否被制
	 * 第二个地支对第一个地支的影响，地支一是否被地支二制
	 * @param  {object} dizhi1 地支对象
	 * @param  {object} dizhi2 地支对象
	 * @return {boolean}        是否被制
	###
	dizhiBeiZhi:(dizhi1,dizhi2)=>
		dizhi1Index=@dizhi.indexOf dizhi1.name
		dizhi2Index=@dizhi.indexOf dizhi2.name
		dizhi1Wuxing=@wuxing.indexOf @dizhiWuxing[@dizhi.indexOf dizhi1.name]
		dizhi2Wuxing=@wuxing.indexOf @dizhiWuxing[@dizhi.indexOf dizhi2.name]
		# 地支2 冲 地支1
		if @dizhiBeiChong dizhi1Index,dizhi2Index
			true
		# 地支2 刑 地支1
		else if @dizhiBeiXing dizhi1Index,dizhi2Index
			true
		# 地支2 克 地支1
		else if @dizhiBeiKe dizhi1Wuxing,dizhi2Wuxing,dizhi1,dizhi2
			true
		# 地支2 泄 地支1
		else if @dizhiBeiXie dizhi1Wuxing,dizhi2Wuxing,dizhi1,dizhi2
			true
		# 地支2 合 地支1，并且地支1减力
		else if @dizhiBeiHe dizhi1Index,dizhi2Index
			true
		else
			false
		
	dizhiRelation:(dizhi1,dizhi2)=>
		score=0
		if @dizhiBeiZhi dizhi1,dizhi2 then score-=1

	genOfYueGanAndNianGan:(YueGan,NianGan)=>

# b=new XinPaiBasic()
# b.dizhiRelation {name:'申'},{name:"戌"}

exports.XinPaiBasic=XinPaiBasic