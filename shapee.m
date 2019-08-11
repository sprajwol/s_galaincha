function [txt, aaa]  = shapee(az, outurl, new_file, onlyfile)
    image = strcat(az, outurl, new_file)
    aaa = strcat("final_", new_file)
    txt = strcat("final_", onlyfile, ".txt")
    outf = strcat(az, outurl, aaa)
    outt = strcat(az, outurl, txt)

    fileID = fopen(outt,'w');

    WB = imread(image);
    BW = imcomplement(WB);
    [B,L,N,A] = bwboundaries(BW);
    imshow(BW); hold on;
    colors=['b' 'g' 'r' 'c' 'm' 'y'];
    
    
    
    for k=1:length(B),
        boundary = B{k};
        cidx = mod(k,length(colors))+1;
        plot(boundary(:,2), boundary(:,1),...
            colors(cidx),'LineWidth',2);

        %randomize text position for better visibility
        rndRow = ceil(length(boundary)/(mod(rand*k,7)+1));
        col = boundary(rndRow,2); row = boundary(rndRow,1);
        h = text(col+1, row-1, num2str(L(row,col)));
        set(h,'Color',colors(cidx),'FontSize',10,'FontWeight','bold');

        props = regionprops(B{k});
        otherArea = sum([props.Area]);

        fprintf(fileID, 'Area of shape %i = %i.\n', k,otherArea)
    end
    fclose(fileID);

    F = getframe;
    imwrite(F.cdata, outf, 'png');
end
