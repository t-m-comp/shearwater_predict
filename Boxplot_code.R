book<-read.table("feature importance\\features_importance_1230_0-5.csv",header=T,sep=",",fill=TRUE, fileEncoding = "GBK")
book_dive<-read.table("trip_duration\\seabird_dives_analysis.csv",header=T,sep=",")

attach(book)
head(book)
attach(book_dive)
head(book_dive)

library(lmerTest)#glmm—pƒ‰ƒCƒuƒ‰ƒŠ
library(ggplot2)


trip_label=book$trip_label
avg_speed=book$avg_speed
std_ori=book$std_ori

sum_dive = book_dive$number_of_sum_dives
single_dive = book_dive$number_of_single_dives
multi_dive = book_dive$number_of_multi_dives
dive_label = book_dive$label



p_std_ori <- ggplot(book,aes(x=trip_label,y=std_ori,fill=trip_label))+ 
  stat_boxplot(geom = "errorbar",width=0.3,aes(color="black"))+ 
  geom_boxplot(size=0.5,fill="white",outlier.fill="white",outlier.color="white")+ 
  geom_jitter(aes(fill=trip_label),width =0.2,shape = 21,size=3)+ 
  scale_fill_manual(values = c("#E69F00", "#0072B2"))+  
  scale_color_manual(values=c("black","black"))+ 
  theme_bw()+ #背景变为白色
  theme(legend.position="none", #不需要图例
        axis.text.x=element_text(colour="black",family="Times",size=30), 
        axis.text.y=element_text(family="Times",size=30,face="plain"), 
        axis.title.y=element_text(family="Times",size = 30,face="plain"), 
        axis.title.x=element_text(family="Times",size = 30,face="plain"), 
        plot.title = element_text(family="Times",size=30,face="bold",hjust = 0.5), 
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())+
  ylab("SD of Orientation")
ggsave("sd_ori.emf", dpi = 300, plot = p_std_ori)

p_avg_speed <- ggplot(book,aes(x=trip_label,y=p_avg_speed,fill=trip_label))+ 
  stat_boxplot(geom = "errorbar",width=0.3,aes(color="black"))+ 
  geom_boxplot(size=0.5,fill="white",outlier.fill="white",outlier.color="white")+ 
  geom_jitter(aes(fill=trip_label),width =0.2,shape = 21,size=3)+ 
  scale_fill_manual(values = c("#E69F00", "#0072B2"))+  
  scale_color_manual(values=c("black","black"))+ 
  theme_bw()+ #背景变为白色
  theme(legend.position="none", #不需要图例
        axis.text.x=element_text(colour="black",family="Times",size=30), 
        axis.text.y=element_text(family="Times",size=30,face="plain"), 
        axis.title.y=element_text(family="Times",size = 30,face="plain"), 
        axis.title.x=element_text(family="Times",size = 30,face="plain"), 
        plot.title = element_text(family="Times",size=30,face="bold",hjust = 0.5), 
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())+
  ylab("Mean speed")
ggsave("avg_speed.emf", dpi = 300, plot = p_avg_speed)

p_dives <- ggplot(book_dive,aes(x=dive_label,y=sum_dive,fill=dive_label))+ 
  stat_boxplot(geom = "errorbar",width=0.3,aes(color="black"))+ 
  geom_boxplot(size=0.5,fill="white",outlier.fill="white",outlier.color="white")+ 
  geom_jitter(aes(fill=dive_label),width =0.2,shape = 21,size=3)+ 
  scale_fill_manual(values = c("#E69F00", "#0072B2"))+ 
  scale_color_manual(values=c("black","black"))+ 
  theme_bw()+ 
  theme(legend.position="none",
        axis.text.x=element_text(colour="black",family="Times",size=30), 
        axis.text.y=element_text(family="Times",size=30,face="plain"), 
        axis.title.y=element_text(family="Times",size = 30,face="plain"), 
        axis.title.x=element_text(family="Times",size = 30,face="plain"), 
        plot.title = element_text(family="Times",size=30,face="bold",hjust = 0.5), 
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())+
  ylab("Number of dives")
ggsave("number_of_dives.emf", dpi = 300, plot = p_dives)

p_single_dive <- ggplot(book_dive,aes(x=dive_label,y=single_dive,fill=dive_label))+ 
  stat_boxplot(geom = "errorbar",width=0.3,aes(color="black"))+ 
  geom_boxplot(size=0.5,fill="white",outlier.fill="white",outlier.color="white")+ 
  geom_jitter(aes(fill=dive_label),width =0.2,shape = 21,size=3)+ 
  scale_fill_manual(values = c("#E69F00", "#0072B2"))+  
  scale_color_manual(values=c("black","black"))+ 

  theme_bw()+
  theme(legend.position="none", 
        axis.text.x=element_text(colour="black",family="Times",size=30), 
        axis.text.y=element_text(family="Times",size=30,face="plain"), 
        axis.title.y=element_text(family="Times",size = 30,face="plain"), 
        axis.title.x=element_text(family="Times",size = 30,face="plain"), 
        plot.title = element_text(family="Times",size=30,face="bold",hjust = 0.5), 
        panel.grid.major = element_blank(), #不显示网格线
        panel.grid.minor = element_blank())+
  ylab("Number of single dives")
ggsave("number_of_single_dives.emf", dpi = 300, plot = p_single_dive)

p_multi_dive <- ggplot(book_dive,aes(x=dive_label,y=multi_dive,fill=dive_label))+ 
  stat_boxplot(geom = "errorbar",width=0.3,aes(color="black"))+ 
  geom_boxplot(size=0.5,fill="white",outlier.fill="white",outlier.color="white")+ 
  geom_jitter(aes(fill=dive_label),width =0.2,shape = 21,size=3)+
  scale_fill_manual(values = c("#E69F00", "#0072B2"))+  
  scale_color_manual(values=c("black","black"))+ 
  theme_bw()+
  theme(legend.position="none", 
        axis.text.x=element_text(colour="black",family="Times",size=30), 
        axis.text.y=element_text(family="Times",size=30,face="plain"), 
        axis.title.y=element_text(family="Times",size = 30,face="plain"), 
        axis.title.x=element_text(family="Times",size = 30,face="plain"),
        plot.title = element_text(family="Times",size=30,face="bold",hjust = 0.5),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())+
  ylab("Number of continuous dives")
ggsave("number_of_continuous_dives.emf", dpi = 300, plot = p_multi_dive)